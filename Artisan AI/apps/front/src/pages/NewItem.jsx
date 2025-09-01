// front/src/pages/NewItem.jsx
import { useNavigate } from 'react-router-dom'
import CreateItemForm from '../components/artisan/CreateItem'

export default function NewItem() {
  const nav = useNavigate()
  return (
    <CreateItemForm
      mode="page"
      onClose={() => nav('/artisan')}
      onCreate={() => nav('/artisan')}
    />
  )
}